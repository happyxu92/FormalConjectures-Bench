import FormalConjectures.Util.ProblemImports
open Classical
open scoped BigOperators
namespace Erdos295
private lemma greedy_tail (a : ℕ) : ∀ b N : ℕ, 0 < b → 0 < N → N * a < b →
    ∃ s : Finset ℕ, (∀ n ∈ s, N < n) ∧ ∑ n ∈ s, (1 / n : ℚ) = (a : ℚ) / b := by
  induction a using Nat.strong_induction_on with
  | h a ih =>
    intro b N hb hN hbound
    by_cases ha : a = 0
    · subst a
      exact ⟨∅, by simp, by simp⟩
    have ha' : 0 < a := Nat.pos_of_ne_zero ha
    let d := (b - 1) / a + 1
    have hmod := Nat.mod_lt (b - 1) ha'
    have hdiv := Nat.mod_add_div (b - 1) a
    have hd : 0 < d := Nat.succ_pos _
    have hbd : b ≤ a * d := by dsimp [d]; rw [Nat.mul_add, Nat.mul_one]; omega
    have hdb : a * d < b + a := by dsimp [d]; rw [Nat.mul_add, Nat.mul_one]; omega
    have hNd : N < d := by nlinarith
    have hab : a < b := by nlinarith
    let r := a * d - b
    have hr : r < a := by dsimp [r]; omega
    have hre : r + b = a * d := Nat.sub_add_cancel hbd
    have hrb : r < b := lt_trans hr hab
    obtain ⟨s, hs, hsum⟩ := ih r hr (b*d) d (Nat.mul_pos hb hd) hd (by nlinarith)
    have hnot : d ∉ s := by intro h; exact (lt_irrefl d) (hs d h)
    refine ⟨insert d s, ?_, ?_⟩
    · intro n hn
      rcases Finset.mem_insert.mp hn with rfl | hn
      · exact hNd
      · exact lt_trans hNd (hs n hn)
    · rw [Finset.sum_insert hnot, hsum]
      have hbq : (b : ℚ) ≠ 0 := by positivity
      have hdq : (d : ℚ) ≠ 0 := by positivity
      have heq : (r : ℚ) + b = (a : ℚ) * d := by exact_mod_cast hre
      push_cast
      field_simp
      nlinarith

private lemma rational_tail (q : ℚ) (N : ℕ) (hN : 0 < N)
    (hq : 0 ≤ q) (hbound : (N : ℚ) * q < 1) :
    ∃ s : Finset ℕ, (∀ n ∈ s, N < n) ∧ ∑ n ∈ s, (1 / n : ℚ) = q := by
  have hnum : 0 ≤ q.num := Rat.num_nonneg.mpr hq
  have heq : ((q.num.toNat : ℕ) : ℚ) / q.den = q := by
    have hc : ((q.num.toNat : ℕ) : ℚ) = (q.num : ℚ) := by
      exact_mod_cast Int.toNat_of_nonneg hnum
    rw [hc, Rat.num_div_den]
  have hd : (0 : ℚ) < q.den := by exact_mod_cast q.pos
  have hb : N * q.num.toNat < q.den := by
    rw [← heq, ← mul_div_assoc, div_lt_iff₀ hd, one_mul] at hbound
    exact_mod_cast hbound
  obtain ⟨s, hs, he⟩ := greedy_tail q.num.toNat q.den N q.pos hN hb
  exact ⟨s, hs, he.trans heq⟩

private lemma unit_tail (N : ℕ) : ∃ s : Finset ℕ,
    (∀ n ∈ s, N < n) ∧ ∑ n ∈ s, (1 / n : ℚ) = 1 := by
  let H : ℕ → ℚ := fun k => ∑ i ∈ Finset.range k, 1 / (N + i + 1 : ℕ)
  have hdiv : Filter.Tendsto (fun k => (H k : ℝ)) Filter.atTop Filter.atTop := by
    have hn : ¬ Summable (fun i : ℕ => (1 / ((i + (N+1) : ℕ) : ℝ))) :=
      fun h => Real.not_summable_one_div_natCast
        ((summable_nat_add_iff (f := fun n : ℕ => 1 / (n : ℝ)) (N+1)).mp h)
    have ht := (not_summable_iff_tendsto_nat_atTop_of_nonneg
      (fun i : ℕ => show (0 : ℝ) ≤ 1 / ((i + (N+1) : ℕ) : ℝ) by positivity)).mp hn
    simpa [H, Nat.cast_add, Nat.cast_one, add_comm, add_left_comm, add_assoc] using ht
  have hex : ∃ k, 1 < H k := by
    obtain ⟨k, hk⟩ := (hdiv.eventually_gt_atTop 1).exists
    exact ⟨k, by exact_mod_cast hk⟩
  let m := Nat.find hex
  have hm : 1 < H m := Nat.find_spec hex
  have hmpos : 0 < m := by
    by_contra h
    have : m = 0 := by omega
    have hh : (1 : ℚ) < 0 := by simpa [this, H] using hm
    norm_num at hh
  obtain ⟨k, hm_eq⟩ := Nat.exists_eq_succ_of_ne_zero (Nat.ne_of_gt hmpos)
  change Nat.find hex = k+1 at hm_eq
  change 1 < H (Nat.find hex) at hm
  rw [hm_eq] at hm
  have hk : H k ≤ 1 := by
    by_contra h
    have hlt := Nat.find_min' hex (lt_of_not_ge h)
    rw [hm_eq] at hlt
    omega
  have hnext : H (k+1) = H k + 1 / (N+k+1 : ℕ) := by
    exact Finset.sum_range_succ _ k
  rw [hnext] at hm
  let q := 1 - H k
  have hq : 0 ≤ q := sub_nonneg.mpr hk
  have hd : (0 : ℚ) < (N+k+1 : ℕ) := by positivity
  have hbound : ((N+k+1 : ℕ) : ℚ) * q < 1 := by
    have hlt : q < 1 / (N+k+1 : ℕ) := by dsimp [q]; linarith
    have hh := (lt_div_iff₀ hd).mp hlt
    simpa [mul_comm] using hh
  obtain ⟨s, hs, he⟩ := rational_tail q (N+k+1) (by omega) hq hbound
  let t := (Finset.range k).image (fun i => N+i+1)
  have ht : ∀ n ∈ t, N < n ∧ n < N+k+1 := by
    intro n hn
    obtain ⟨i, hi, rfl⟩ := Finset.mem_image.mp hn
    have := Finset.mem_range.mp hi
    omega
  have hdis : Disjoint t s := by
    apply Finset.disjoint_left.mpr
    intro n hn hns
    have := ht n hn
    have := hs n hns
    omega
  refine ⟨t ∪ s, ?_, ?_⟩
  · intro n hn
    rcases Finset.mem_union.mp hn with hn | hn
    · exact (ht n hn).1
    · exact lt_trans (by omega) (hs n hn)
  · rw [Finset.sum_union hdis, he]
    have htsum : ∑ n ∈ t, (1 / n : ℚ) = H k := by
      apply Finset.sum_image
      intro i hi j hj hij
      dsimp at hij
      omega
    rw [htsum]
    dsimp [q]
    ring

lemma exists_k (N : ℕ) : ∃ (k : ℕ) (n : Fin k.succ → ℕ),
    (∀ i, N ≤ n i) ∧ StrictMono n ∧ ∑ i, (1 / n i : ℝ) = 1 := by
  obtain ⟨s, hs, he⟩ := unit_tail N
  have hne : s.Nonempty := by
    by_contra h
    have hempty : s = ∅ := Finset.not_nonempty_iff_eq_empty.mp h
    rw [hempty] at he
    norm_num at he
  obtain ⟨k, hk⟩ := Nat.exists_eq_succ_of_ne_zero (Nat.ne_of_gt (Finset.card_pos.mpr hne))
  let n := s.orderEmbOfFin hk
  refine ⟨k, n, ?_, n.strictMono, ?_⟩
  · intro i
    exact (hs (n i) (s.orderEmbOfFin_mem hk i)).le
  · have hsum : ∑ i : Fin k.succ, (1 / n i : ℚ) = 1 := by
      calc
        ∑ i : Fin k.succ, (1 / n i : ℚ) = ∑ x ∈ Finset.univ.image n, (1 / x : ℚ) :=
          (Finset.sum_image (s := Finset.univ) (g := n) (f := fun x : ℕ => (1 / x : ℚ))
            (fun i hi j hj h => n.injective h)).symm
        _ = ∑ x ∈ s, (1 / x : ℚ) := by rw [s.image_orderEmbOfFin_univ hk]
        _ = 1 := he
    have hr := congrArg (fun q : ℚ => (q : ℝ)) hsum
    simpa only [Rat.cast_sum, Rat.cast_div, Rat.cast_one, Rat.cast_natCast] using hr

#print axioms exists_k
end Erdos295
